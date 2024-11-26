import { useState, useEffect, createContext } from "react";
// Util
import { v4 as uuidv4 } from "uuid";

export interface NotificationParam {
  type: "WARNING" | "ERROR" | "INFO" | "SUCCESS";
  message: string;
}

export interface Notification extends NotificationParam {
  id: string;
}

type NotificationContextType = (n: NotificationParam) => void;

const MESSAGE_LIFETIME = 2;
const MAX_NOTIFICATIONS = 3;

export const NotificationContext = createContext<NotificationContextType>(
  (_) => {},
);

const useNotification = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (notification: NotificationParam) => {
    if (notifications.length >= MAX_NOTIFICATIONS) {
      notifications.shift();
    }
    setNotifications([...notifications, { id: uuidv4(), ...notification }]);
  };

  useEffect(() => {
    const id = setTimeout(() => {
      notifications.shift();
      setNotifications([...notifications]);
    }, MESSAGE_LIFETIME * 1000);
    return () => {
      clearTimeout(id);
    };
  }, [notifications]);

  return { notifications, addNotification };
};

export default useNotification;
