
/* ==================================================
   MediSync - Main JavaScript

   Features:
   1. Active navigation highlighting
   2. Form validation
   3. Prevent duplicate form submissions
   4. Toast notifications
   5. Medicine reminders
   6. Appointment reminders
   ================================================== */


/* ==================================================
   1. TOAST NOTIFICATIONS
   ================================================== */

window.mediSyncToast = function (message) {
    let toast = document.getElementById("medisync-toast");

    if (!toast) {
        toast = document.createElement("div");
        toast.id = "medisync-toast";
        toast.setAttribute("role", "status");
        toast.setAttribute("aria-live", "polite");

        Object.assign(toast.style, {
            position: "fixed",
            bottom: "20px",
            right: "20px",
            maxWidth: "min(360px, calc(100vw - 40px))",
            padding: "14px 18px",
            background: "#115e59",
            color: "#ffffff",
            borderRadius: "12px",
            boxShadow: "0 8px 24px rgba(0,0,0,.15)",
            zIndex: "9999",
            fontSize: "14px",
            lineHeight: "1.5"
        });

        document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.hidden = false;

    clearTimeout(window.mediSyncToastTimer);

    window.mediSyncToastTimer = setTimeout(function () {
        toast.hidden = true;
    }, 5000);
};


/* ==================================================
   2. DASHBOARD INITIALIZATION
   ================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ----------------------------------------------
       Active navigation highlighting
       ---------------------------------------------- */

    const currentPath =
        window.location.pathname.replace(/\/+$/, "") || "/";

    document.querySelectorAll("nav a, .sidebar a").forEach(function (link) {
        try {
            const linkPath =
                new URL(link.href, window.location.origin)
                    .pathname.replace(/\/+$/, "") || "/";

            if (linkPath === currentPath) {
                link.classList.add("active");
                link.setAttribute("aria-current", "page");
            }
        } catch (error) {
            console.warn("Could not process navigation link:", error);
        }
    });


    /* ----------------------------------------------
       Form validation and duplicate-submit prevention
       ---------------------------------------------- */

    document.querySelectorAll("form").forEach(function (form) {

        form.addEventListener("submit", function (event) {

            if (!form.checkValidity()) {
                event.preventDefault();
                form.reportValidity();
                return;
            }

            const submitButton = event.submitter;

            if (submitButton && !submitButton.disabled) {
                submitButton.dataset.originalText =
                    submitButton.value || submitButton.textContent || "";

                submitButton.disabled = true;

                if (submitButton.tagName === "INPUT") {
                    submitButton.value = "Please wait...";
                } else {
                    submitButton.textContent = "Please wait...";
                }
            }
        });
    });


    /* ----------------------------------------------
       Read reminder data safely
       ---------------------------------------------- */

    function readReminderData(elementId) {
        const element = document.getElementById(elementId);

        if (!element) {
            return [];
        }

        try {
            const data = JSON.parse(element.textContent);

            if (!Array.isArray(data)) {
                console.error(elementId + " must contain an array.");
                return [];
            }

            return data;

        } catch (error) {
            console.error(
                "Could not read reminder data:",
                elementId,
                error
            );

            return [];
        }
    }

    const medicines = readReminderData("medicine-reminder-data");
    const appointments = readReminderData("appointment-reminder-data");


    /* ----------------------------------------------
       Date and time helpers
       ---------------------------------------------- */

    function getLocalDateString(dateObject) {
        return [
            dateObject.getFullYear(),
            String(dateObject.getMonth() + 1).padStart(2, "0"),
            String(dateObject.getDate()).padStart(2, "0")
        ].join("-");
    }

    function getLocalTimeString(dateObject) {
        return [
            String(dateObject.getHours()).padStart(2, "0"),
            String(dateObject.getMinutes()).padStart(2, "0")
        ].join(":");
    }


    /* ----------------------------------------------
       Prevent duplicate notifications in this page
       session
       ---------------------------------------------- */

    const notifiedReminders = new Set();


    /* ==================================================
       3. MEDICINE REMINDERS
       ================================================== */

    function checkMedicineReminders() {
        const now = new Date();

        const currentDate = getLocalDateString(now);
        const currentTime = getLocalTimeString(now);

        medicines.forEach(function (medicine) {

            // Only remind during the medicine's date range.
            if (
                currentDate < medicine.start_date ||
                currentDate > medicine.end_date
            ) {
                return;
            }

            const reminderKey =
                "medicine-" + medicine.id + "-" + currentDate;

            if (
                medicine.reminder_time === currentTime &&
                !notifiedReminders.has(reminderKey)
            ) {
                notifiedReminders.add(reminderKey);

                window.mediSyncToast(
                    "Medicine reminder: " +
                    medicine.name +
                    " (" +
                    medicine.dosage +
                    "). Please follow your prescribed schedule."
                );

                console.log(
                    "MediSync medicine reminder triggered:",
                    medicine.name
                );
            }
        });
    }


    /* ==================================================
       4. APPOINTMENT REMINDERS
       ================================================== */

    function checkAppointmentReminders() {
        const now = new Date();

        appointments.forEach(function (appointment) {

            if (
                !appointment.appointment_date ||
                !appointment.appointment_time
            ) {
                return;
            }

            // Parse the appointment's local date and time.
            const appointmentDateTime = new Date(
                appointment.appointment_date +
                "T" +
                appointment.appointment_time +
                ":00"
            );

            if (Number.isNaN(appointmentDateTime.getTime())) {
                console.warn(
                    "Invalid appointment date or time:",
                    appointment
                );
                return;
            }

            // Notify once when the appointment is approximately
            // 30 minutes away.
            const minutesUntilAppointment =
                (appointmentDateTime.getTime() - now.getTime()) /
                60000;

            if (
                minutesUntilAppointment > 0 &&
                minutesUntilAppointment <= 30 &&
                minutesUntilAppointment > 29
            ) {
                const reminderKey =
                    "appointment-" + appointment.id;

                if (!notifiedReminders.has(reminderKey)) {
                    notifiedReminders.add(reminderKey);

                    window.mediSyncToast(
                        "Appointment reminder: Your appointment with " +
                        appointment.doctor_name +
                        " at " +
                        appointment.hospital_name +
                        " is in approximately 30 minutes."
                    );

                    console.log(
                        "MediSync appointment reminder triggered:",
                        appointment.doctor_name
                    );
                }
            }
        });
    }


    /* ==================================================
       5. START REMINDER CHECKER
       ================================================== */

    function checkAllReminders() {
        checkMedicineReminders();
        checkAppointmentReminders();
    }

    console.log("MediSync reminder checker is running.");

    checkAllReminders();

    // Check every minute while this page remains open.
    window.setInterval(checkAllReminders, 60 * 1000);


    /* ==================================================
       6. TEST NOTIFICATION BUTTON
       ================================================== */

    const testButton =
        document.getElementById("test-notification-btn");

    if (testButton) {
        testButton.addEventListener("click", function () {
            window.mediSyncToast(
                "Test notification: MediSync notifications are working!"
            );
        });
    }

});

