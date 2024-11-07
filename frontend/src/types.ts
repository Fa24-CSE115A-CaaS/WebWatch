export interface TaskResponse {
  id: number;
  name: string;
  content?: string;
  url: string;
  discord_url?: string;
  enabled_notification_options: string[];
  enabled: boolean;
}

export interface Task {
  id: number;
  name: string;
  content?: string;
  url: string;
  discordUrl?: string;
  enabledNotificationOptions: string[];
  enabled: boolean;
}
