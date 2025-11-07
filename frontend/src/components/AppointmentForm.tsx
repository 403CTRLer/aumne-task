import { ChangeEvent, FormEvent, useState } from "react";

import type { CreateAppointmentPayload } from "../types";

interface AppointmentFormProps {
  onSubmit: (payload: CreateAppointmentPayload) => Promise<void>;
  isSubmitting: boolean;
}

const initialState: CreateAppointmentPayload = {
  user_name: "",
  phone_number: "",
  reason: "",
  appointment_time: "",
};

export function AppointmentForm({ onSubmit, isSubmitting }: AppointmentFormProps) {
  // Keep the form controlled so we can easily reset and validate fields.
  const [formData, setFormData] = useState<CreateAppointmentPayload>(initialState);

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    await onSubmit(formData);
    setFormData(initialState);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Full name
        <input
          name="user_name"
          placeholder="Jane Doe"
          value={formData.user_name}
          onChange={handleChange}
          required
        />
      </label>

      <label>
        WhatsApp phone number (include country code)
        <input
          name="phone_number"
          placeholder="whatsapp:+15555555555"
          value={formData.phone_number}
          onChange={handleChange}
          required
        />
      </label>

      <label>
        Reason
        <textarea
          name="reason"
          placeholder="Describe the purpose of the visit"
          value={formData.reason}
          onChange={handleChange}
          rows={3}
          required
        />
      </label>

      <label>
        Appointment time
        <input
          type="datetime-local"
          name="appointment_time"
          value={formData.appointment_time}
          onChange={handleChange}
          required
        />
      </label>

      <button className="primary" type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Scheduling..." : "Schedule appointment"}
      </button>
    </form>
  );
}

