import { format } from "date-fns";

import type { Appointment } from "../types";

interface AppointmentListProps {
  appointments: Appointment[];
  onCancel: (appointmentId: number) => Promise<void>;
  cancelingId: number | null;
}

export function AppointmentList({ appointments, onCancel, cancelingId }: AppointmentListProps) {
  if (!appointments.length) {
    return <p>No appointments scheduled yet.</p>;
  }

  return (
    <div className="appointment-list">
      {appointments.map((appointment) => {
        // Format timestamps once per item so the template stays tidy.
        const appointmentDate = format(new Date(appointment.appointment_time), "PPpp");
        const createdAt = format(new Date(appointment.created_at), "PPpp");
        const isCanceled = appointment.status === "canceled";
        const isCanceling = cancelingId === appointment.id;

        return (
          <article key={appointment.id} className="appointment-item">
            <div className="appointment-header">
              <div>
                <h3>{appointment.user_name}</h3>
                <small>{appointment.phone_number}</small>
              </div>
              <span className={`status ${appointment.status}`}>{appointment.status}</span>
            </div>

            <div className="metainfo">
              <span>
                <strong>When:</strong> {appointmentDate}
              </span>
              <span>
                <strong>Reason:</strong> {appointment.reason}
              </span>
              <span>
                <strong>Created:</strong> {createdAt}
              </span>
              <span>
                <strong>Reminder sent:</strong> {appointment.reminder_sent ? "Yes" : "No"}
              </span>
            </div>

            <div>
              <button
                className="secondary"
                disabled={isCanceled || isCanceling}
                onClick={() => onCancel(appointment.id)}
              >
                {isCanceled ? "Already canceled" : isCanceling ? "Canceling..." : "Cancel appointment"}
              </button>
            </div>
          </article>
        );
      })}
    </div>
  );
}

