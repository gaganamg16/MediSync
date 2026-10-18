from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST


@login_required
def chatbot_page(request):
    return render(request, "ai_assistant/chatbot.html")


def get_health_response(message):
    """
    Return predefined health FAQ responses.
    This is a demo FAQ system, not a live AI model.
    """
    text = message.lower().strip()

    # Greetings
    if any(word in text for word in ["hello", "hi", "hey"]):
        return (
            "Hello! Welcome to MediSync Health FAQ. "
            "You can ask me about hydration, sleep, medicine safety, "
            "appointments, and general health education."
        )

    # Hydration
    if any(word in text for word in [
        "water", "hydration", "hydrated", "drink water"
    ]):
        return (
            "HEALTH FAQ — HYDRATION\n\n"
            "Drinking water regularly throughout the day can help maintain "
            "hydration. Your needs vary with activity, weather, and health "
            "conditions. Follow any fluid restrictions advised by your "
            "healthcare professional."
        )

    # Sleep
    if any(word in text for word in [
        "sleep", "sleeping", "insomnia", "rest", "bedtime"
    ]):
        return (
            "HEALTH FAQ — SLEEP\n\n"
            "A regular sleep schedule, a comfortable sleep environment, "
            "and a relaxing bedtime routine may support healthy sleep. "
            "If sleep difficulties continue, consult a healthcare professional."
        )

    # Medicine safety
    if any(word in text for word in [
        "medicine", "medication", "tablet", "drug", "dose", "dosage"
    ]):
        return (
            "HEALTH FAQ — MEDICINE SAFETY\n\n"
            "Take medicines only as directed by a qualified healthcare "
            "professional or according to the official instructions. "
            "Do not change a prescribed dose or combine medicines without "
            "checking with a healthcare professional or pharmacist."
        )

    # Appointments
    if any(word in text for word in [
        "appointment", "doctor visit", "hospital visit"
    ]):
        return (
            "HEALTH FAQ — APPOINTMENTS\n\n"
            "Before a medical appointment, consider noting your questions, "
            "current medicines, allergies, and relevant symptoms. Bring "
            "any medical information your healthcare professional requests. "
            "You can manage your appointments through the MediSync dashboard."
        )

    # Healthy habits
    if any(word in text for word in [
        "exercise", "physical activity", "fitness", "healthy habits"
    ]):
        return (
            "HEALTH FAQ — HEALTHY HABITS\n\n"
            "Regular physical activity suited to your abilities, balanced "
            "meals, sufficient sleep, and hydration can support general "
            "well-being. Start at a comfortable level and seek professional "
            "advice if you have health concerns."
        )

    # Nutrition
    if any(word in text for word in [
        "food", "nutrition", "diet", "fruits", "vegetables"
    ]):
        return (
            "HEALTH FAQ — NUTRITION\n\n"
            "A varied eating pattern that includes fruits, vegetables, "
            "grains, protein sources, and other foods appropriate to your "
            "needs can support general health. Individual nutritional needs "
            "vary, so consult a qualified professional for personalized advice."
        )

    # Fever and symptoms
    if any(word in text for word in [
        "fever", "pain", "symptom", "sick", "illness"
    ]):
        return (
            "HEALTH FAQ — SYMPTOMS\n\n"
            "Symptoms can have many causes, and this FAQ cannot diagnose "
            "them. Contact a qualified healthcare professional for advice "
            "about your symptoms. Seek urgent medical care for severe or "
            "rapidly worsening symptoms."
        )

    # Stress and relaxation
    if any(word in text for word in [
        "stress", "relax", "anxiety", "tension"
    ]):
        return (
            "HEALTH FAQ — STRESS MANAGEMENT\n\n"
            "Taking breaks, maintaining a regular routine, talking to "
            "someone you trust, and trying calm breathing exercises may "
            "help with everyday stress. If distress persists or affects "
            "daily life, consider speaking with a qualified professional."
        )

    # Medical records
    if any(word in text for word in [
        "medical record", "health record", "health history", "report"
    ]):
        return (
            "HEALTH FAQ — MEDICAL RECORDS\n\n"
            "Keeping medical records organized can help you and your "
            "healthcare professional review relevant health information. "
            "MediSync provides a Medical Records section where you can "
            "manage records in your application."
        )

    # Emergencies
    if any(word in text for word in [
        "emergency", "urgent", "can't breathe", "cannot breathe"
    ]):
        return (
            "URGENT HEALTH NOTICE\n\n"
            "If you or someone else may be experiencing a medical emergency, "
            "contact your local emergency service or go to the nearest "
            "emergency department immediately. Do not wait for a chatbot "
            "response."
        )

    # Default response
    return (
        "I couldn't find a matching topic in the MediSync Health FAQ yet.\n\n"
        "Try asking about:\n"
        "• Hydration and drinking water\n"
        "• Sleep and rest\n"
        "• Medicine safety\n"
        "• Doctor appointments\n"
        "• Nutrition and healthy habits\n"
        "• Stress management\n"
        "• Symptoms and medical records\n\n"
        "This is a predefined FAQ system, not a live AI model."
    )


@login_required
@require_POST
def chatbot_response(request):
    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse(
            {"error": "Please enter a message."},
            status=400
        )

    if len(message) > 2000:
        return JsonResponse(
            {"error": "Please keep your message under 2000 characters."},
            status=400
        )

    answer = get_health_response(message)

    return JsonResponse({
        "answer": answer,
        "mode": "faq"
    })

