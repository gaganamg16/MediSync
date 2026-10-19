
import logging
import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from google import genai

from .models import ChatConversation, ChatMessage


logger = logging.getLogger(__name__)

@login_required
def chatbot_page(request):
    conversations = ChatConversation.objects.filter(
        user=request.user
    )

    conversation_id = request.GET.get("conversation")
    current_conversation = None
    messages = []

    if conversation_id:
        current_conversation = get_object_or_404(
            ChatConversation,
            id=conversation_id,
            user=request.user,
        )

        messages = current_conversation.messages.all()

    return render(
        request,
        "ai_assistant/chatbot.html",
        {
            "conversations": conversations,
            "current_conversation": current_conversation,
            "messages": messages,
        },
    )



def get_gemini_response(message):
    """Generate a general health-information response using Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("The Gemini API key is not configured.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are MediSync AI, a health information assistant.

Follow these rules:

1. Provide general health education in simple, clear language.
2. Do not diagnose diseases or prescribe medicines.
3. Never recommend changing a prescribed medicine dose.
4. Encourage users to consult qualified healthcare professionals
   for personal medical concerns.
5. For potentially serious symptoms, advise prompt medical assessment.
6. For possible medical emergencies, advise contacting local emergency
   services immediately. In India, the emergency number is 112.
7. Do not claim to access medical records or patient information.
8. If uncertain, say so instead of inventing medical facts.
9. Keep answers concise, supportive, and easy to understand.

User's message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    answer = response.text

    if not answer:
        raise RuntimeError("Gemini returned an empty response.")

    return answer


@login_required
@require_POST
def chatbot_response(request):
    message = request.POST.get("message", "").strip()
    conversation_id = request.POST.get("conversation_id", "").strip()

    if not message:
        return JsonResponse(
            {"error": "Please enter a message."},
            status=400,
        )

    if len(message) > 2000:
        return JsonResponse(
            {"error": "Please keep your message under 2000 characters."},
            status=400,
        )

    # Find the user's existing conversation or create a new one.
    if conversation_id:
        conversation = get_object_or_404(
            ChatConversation,
            id=conversation_id,
            user=request.user,
        )
    else:
        conversation = ChatConversation.objects.create(
            user=request.user,
            title=message[:60],
        )

    # Save the user's message before requesting an AI response.
    ChatMessage.objects.create(
        conversation=conversation,
        role="user",
        content=message,
    )

    try:
        answer = get_gemini_response(message)

        # Save Gemini's response.
        ChatMessage.objects.create(
            conversation=conversation,
            role="assistant",
            content=answer,
        )

        conversation.save()

        return JsonResponse(
            {
                "answer": answer,
                "mode": "gemini",
                "conversation_id": conversation.id,
            }
        )

    except Exception:
        logger.exception("MediSync Gemini request failed.")

        return JsonResponse(
            {
                "error": (
                    "The AI assistant is temporarily unavailable. "
                    "Your message has been saved. Please try again."
                ),
                "conversation_id": conversation.id,
            },
            status=503,
        )

@login_required
@require_POST
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(
        ChatConversation,
        id=conversation_id,
        user=request.user,
    )

    conversation.delete()

    return redirect("chatbot_page")
