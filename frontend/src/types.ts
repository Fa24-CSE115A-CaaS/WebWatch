export interface TaskResponse {
  id: number;
  name: string;
  content?: string;
  url: string;
  discord_url?: string;
  interval: number;
  enabled_notification_options: string[];
  enabled: boolean;
  next_run: string;
  xpath: string | null;
}

export interface Task {
  id: number;
  name: string;
  content?: string;
  url: string;
  discordUrl?: string;
  interval: number;
  enabledNotificationOptions: string[];
  enabled: boolean;
  nextRun: Date;
  xpath: string;
}
