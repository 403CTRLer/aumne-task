import { useEffect, useMemo, useState } from "react";

import { AppointmentForm } from "./components/AppointmentForm";
import { AppointmentList } from "./components/AppointmentList";
import { cancelAppointment, createAppointment, listAppointments } from "./api";
import type { Appointment, CreateAppointmentPayload } from "./types";

type FeedbackState = { type: "error" | "success"; message: string } | null;

export default function App() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [cancelingId, setCancelingId] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<FeedbackState>(null);

  const loadAppointments = async () => {
    setIsLoading(true);
    try {
      const data = await listAppointments();
      setAppointments(data);
    } catch (error) {
      console.error(error);
      setFeedback({ type: "error", message: "Failed to load appointments." });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Load the dashboard data on mount.
    loadAppointments();
  }, []);

  const handleSchedule = async (payload: CreateAppointmentPayload) => {
    setIsSubmitting(true);
    setFeedback(null);
    try {
      const created = await createAppointment(payload);
      setAppointments((existing) => [...existing, created]);
      setFeedback({ type: "success", message: "Appointment scheduled successfully." });
    } catch (error: any) {
      const message = error?.response?.data?.detail ?? "Unable to schedule appointment.";
      setFeedback({ type: "error", message });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancel = async (appointmentId: number) => {
    setFeedback(null);
    setCancelingId(appointmentId);
    try {
      await cancelAppointment(appointmentId);
      setAppointments((existing) =>
        existing.map((appointment) =>
          appointment.id === appointmentId
            ? { ...appointment, status: "canceled" }
            : appointment
        )
      );
      setFeedback({ type: "success", message: "Appointment canceled." });
    } catch (error: any) {
      const message = error?.response?.data?.detail ?? "Failed to cancel appointment.";
      setFeedback({ type: "error", message });
    } finally {
      setCancelingId(null);
    }
  };

  const sortedAppointments = useMemo(
    () =>
      // Copy the array before sorting to avoid mutating state directly.
      [...appointments].sort(
        (a, b) => new Date(a.appointment_time).getTime() - new Date(b.appointment_time).getTime()
      ),
    [appointments]
  );

  return (
    <div className="app-container">
      <h1>WhatsApp Appointment Dashboard</h1>

      <div className="grid">
        <section className="card">
          <h2>Schedule new appointment</h2>
          <AppointmentForm onSubmit={handleSchedule} isSubmitting={isSubmitting} />
        </section>

        <section className="card">
          <h2>Upcoming appointments</h2>
          {isLoading ? (
            <p>Loading appointments...</p>
          ) : (
            <AppointmentList appointments={sortedAppointments} onCancel={handleCancel} cancelingId={cancelingId} />
          )}
        </section>
      </div>

      {feedback && <div className={`feedback ${feedback.type}`}>{feedback.message}</div>}
    </div>
  );
}

