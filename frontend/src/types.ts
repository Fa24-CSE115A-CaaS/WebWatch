export interface TaskResponse {
  id: number;
  name: string;
  content?: string;
  url: string;
  discord_url?: string;
  slack_url?: string;
  interval: number;
  enabled_notification_options: string[];
  enabled: boolean;
  next_run: string;
}

export interface Task {
  id: number;
  name: string;
  content?: string;
  url: string;
  discordUrl?: string;
  slackUrl?: string;
  interval: number;
  enabledNotificationOptions: string[];
  enabled: boolean;
  nextRun: Date;
}
