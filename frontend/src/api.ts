import axios from "axios";

import type { Appointment, CreateAppointmentPayload } from "./types";

const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const client = axios.create({
  baseURL,
});

export async function createAppointment(payload: CreateAppointmentPayload) {
  // POST is used so the backend can validate and persist the appointment.
  const { data } = await client.post<Appointment>("/appointments/", payload);
  return data;
}

export async function listAppointments() {
  // Fetch every upcoming appointment for the dashboard.
  const { data } = await client.get<Appointment[]>("/appointments/");
  return data;
}

export async function cancelAppointment(appointmentId: number) {
  // Cancel the appointment in place; no response body expected.
  await client.delete(`/appointments/${appointmentId}`);
}

