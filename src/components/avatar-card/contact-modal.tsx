// components/contact-modal.tsx
import React from 'react';
import { Profile } from '../../interfaces/profile';

interface ContactModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: Profile;
}

const ContactModal: React.FC<ContactModalProps> = ({
  isOpen,
  onClose,
  profile,
}) => {
  if (!isOpen) return null;

  const downloadContact = () => {
    const vCard = `BEGIN:VCARD
VERSION:3.0
FN:James Brendamour
EMAIL:James@bmours.com
TEL:513-543-8687
URL:https://www.linkedin.com/in/jamesbmour/
END:VCARD`;

    const blob = new Blob([vCard], { type: 'text/vcard' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${profile.name}.vcf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="p-6 rounded-lg shadow-xl bg-base-100">
        <h3 className="mb-4 text-lg font-bold">Contact Information</h3>
        <div className="space-y-2">
          {profile.contact?.email && (
            <p>
              Email:{' '}
              <a href={`mailto:${profile.contact.email}`} className="link">
                {profile.contact.email}
              </a>
            </p>
          )}
          {profile.contact?.phone && (
            <p>
              Phone:{' '}
              <a href={`tel:${profile.contact.phone}`} className="link">
                {profile.contact.phone}
              </a>
            </p>
          )}
          {profile.contact?.linkedin && (
            <p>
              LinkedIn:{' '}
              <a
                href={profile.contact.linkedin}
                target="_blank"
                rel="noreferrer"
                className="link"
              >
                Profile
              </a>
            </p>
          )}
        </div>
        <div className="flex justify-end gap-2 mt-4">
          <button className="btn btn-sm" onClick={downloadContact}>
            Download vCard
          </button>
          <button className="btn btn-sm btn-primary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ContactModal;
