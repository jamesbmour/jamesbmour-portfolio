export interface Profile {
  avatar: string;
  name: string;
  bio?: string;
  location?: string;
  company?: string;
  contact?: {
    email?: string;
    phone?: string;
    linkedin?: string;
  };
}
