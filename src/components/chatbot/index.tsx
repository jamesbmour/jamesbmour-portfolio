import { BubbleChat } from 'flowise-embed-react';

const Chatbot = () => {
  return (
    <BubbleChat
      chatflowid="e2b4942e-e94c-423e-9483-33f13d9496f4"
      apiHost="https://flowise.jdb7.us"
      theme={{
        button: {
          backgroundColor: '#1c4976',
          right: 20,
          bottom: 20,
          size: 'medium',
          iconColor: 'white',
          customIconSrc:
            'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-messages.svg',
        },
        chatWindow: {
          welcomeMessage: 'Hello! Chat with James Brendamour Resume',
          backgroundColor: '#ffffff',
          height: 700,
          width: 400,
          fontSize: 16,
          poweredByTextColor: '#ffffff',
          botMessage: {
            backgroundColor: '#f7f8ff',
            textColor: '#303235',
            showAvatar: true,
            avatarSrc: 'https://avatars.githubusercontent.com/u/22489672?v=4',
          },
          userMessage: {
            backgroundColor: '#3B81F6',
            textColor: '#ffffff',
            showAvatar: true,
            avatarSrc:
              'https://raw.githubusercontent.com/zahidkhawaja/langchain-chat-nextjs/main/public/usericon.png',
          },
          textInput: {
            placeholder: 'Type your question',
            backgroundColor: '#ffffff',
            textColor: '#303235',
            sendButtonColor: '#3B81F6',
          },
        },
      }}
    />

    // <BubbleChat
    //   chatflowid="e2b4942e-e94c-423e-9483-33f13d9496f4"
    //   apiHost="https://flowise.jdb7.us"
    //   theme={{
    //     button: {
    //       backgroundColor: '#1c4976',
    //       right: 20,
    //       bottom: 20,
    //       size: 48, // small | medium | large | number
    //       dragAndDrop: true,
    //       iconColor: 'white',
    //       customIconSrc:
    //         'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-messages.svg',
    //       autoWindowOpen: {
    //         autoOpen: true, //parameter to control automatic window opening
    //         openDelay: 2, // Optional parameter for delay time in seconds
    //         autoOpenOnMobile: false, //parameter to control automatic window opening in mobile
    //       },
    //     },
    //     tooltip: {
    //       showTooltip: true,
    //       tooltipMessage: 'Chat with my resume!',
    //       tooltipBackgroundColor: 'black',
    //       tooltipTextColor: 'white',
    //       tooltipFontSize: 16,
    //     },
    //     chatWindow: {
    //       showTitle: true,
    //       title: 'James Bot',

    //       titleAvatarSrc:
    //         'https://raw.githubusercontent.com/walkxcode/dashboard-icons/main/svg/google-messages.svg',
    //       showAgentMessages: true,
    //       welcomeMessage: 'Hello! What would you like to know?',
    //       errorMessage: 'This is a custom error message',
    //       backgroundColor: '#ffffff',
    //       backgroundImage: 'enter image path or link', // If set, this will overlap the background color of the chat window.
    //       height: 700,
    //       width: 400,
    //       fontSize: 16,
    //       //starterPrompts: ['What is a bot?', 'Who are you?'], // It overrides the starter prompts set by the chat flow passed
    //       starterPromptFontSize: 15,
    //       clearChatOnReload: false, // If set to true, the chat will be cleared when the page reloads.
    //       botMessage: {
    //         backgroundColor: '#f7f8ff',
    //         textColor: '#303235',
    //         showAvatar: true,
    //         avatarSrc:
    //           'https://raw.githubusercontent.com/zahidkhawaja/langchain-chat-nextjs/main/public/parroticon.png',
    //       },
    //       userMessage: {
    //         backgroundColor: '#3B81F6',
    //         textColor: '#ffffff',
    //         showAvatar: true,
    //         avatarSrc:
    //           'https://raw.githubusercontent.com/zahidkhawaja/langchain-chat-nextjs/main/public/usericon.png',
    //       },
    //       textInput: {
    //         placeholder: 'Type your question',
    //         backgroundColor: '#ffffff',
    //         textColor: '#303235',
    //         sendButtonColor: '#3B81F6',
    //         maxChars: 50,
    //         maxCharsWarningMessage:
    //           'You exceeded the characters limit. Please input less than 50 characters.',
    //         autoFocus: true, // If not used, autofocus is disabled on mobile and enabled on desktop. true enables it on both, false disables it on both.
    //         sendMessageSound: true,
    //         // sendSoundLocation: "send_message.mp3", // If this is not used, the default sound effect will be played if sendSoundMessage is true.
    //         receiveMessageSound: true,
    //         // receiveSoundLocation: "receive_message.mp3", // If this is not used, the default sound effect will be played if receiveSoundMessage is true.
    //       },
    //       feedback: {
    //         color: '#303235',
    //       },
    //       footer: {
    //         textColor: '#303235',
    //         text: 'Powered by',
    //         company: 'Flowise',
    //         companyLink: 'https://flowiseai.com',
    //       },
    //       poweredByTextColor: '#ff0000',
    //     },
    //   }}
    // />
  );
};

export default Chatbot;
