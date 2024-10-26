export interface Task {
  id: number;
  name: string;
  content?: string;
  url: string;
  discordUrl?: string;
  enabledNotificationOptions: string[];
  enabled: boolean;
}