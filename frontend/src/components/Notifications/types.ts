import { FunctionComponent } from "react";
// Types
import { Notification } from "../../hooks/useNotification";

interface NotificationsProps {
  notifications: Notification[];
}

export type NotificationsComponent = FunctionComponent<NotificationsProps>;
