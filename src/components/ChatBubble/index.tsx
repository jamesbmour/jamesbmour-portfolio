import React, { useState, RefObject } from 'react'

export const ChatBubble = ( props: { getMessage?: any; messages?: any } ) => {
    let hide = {
        display: 'none',
    }
    let show = {
        display: 'block'
    }
    let textRef: RefObject<HTMLInputElement> = React.createRef()
    const {messages} = props

    const [chatopen, setChatopen] = useState(false)
    const toggle = () => {
        setChatopen(!chatopen)
    }

    const handleSend = () => {
        const get = props.getMessage
        get((textRef.current as HTMLInputElement).value)
    }

    return (
        <div id='chatCon'>
            <div className="chat-box" style={chatopen ? show : hide}>
                <div className="header">Chat with me</div>
                <div className="msg-area">
                    {
                        messages.map((msg: string | number | boolean | React.ReactElement<any, string | React.JSXElementConstructor<any>> | Iterable<React.ReactNode> | null | undefined, i: number) => (
                            i%2 ? (
                                <p className="right"><span>{ msg }</span></p>
                            ) : (
                                <p className="left"><span>{ msg }</span></p>
                            )
                        ))
                    }
                </div>
                <div className="footer">
                    <button onClick={handleSend}><i className="fa fa-paper-plane"></i></button>
                </div>
            </div>
            <div className="pop">
                <p><img onClick={toggle} src="https://p7.hiclipart.com/preview/151/758/442/iphone-imessage-messages-logo-computer-icons-message.jpg" alt="" /></p>
            </div>
        </div>
    )
}

export default ChatBubble
