export type AppointmentStatus = "confirmed" | "canceled";

export interface Appointment {
  // Mirrors the API response shape.
  id: number;
  user_name: string;
  phone_number: string;
  reason: string;
  appointment_time: string;
  status: AppointmentStatus;
  reminder_sent: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateAppointmentPayload {
  // Payload used by the scheduler form.
  user_name: string;
  phone_number: string;
  reason: string;
  appointment_time: string;
}

