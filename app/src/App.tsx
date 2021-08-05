import React, {useEffect, useState} from 'react';
import {io} from "socket.io-client";
import './App.css';
import ReactPlayer from 'react-player';

function App() {

    const [videoIdxQueue] = useState<Array<number>>([]);
    const [playingDefault, setPlayingDefault] = useState<boolean>(true);
    const [counter, setCounter] = useState<number>(0);

    useEffect(() => {
        const socket = io("http://localhost:5000");
        socket.on('video_queued', ({video_idx}) => {
            videoIdxQueue.push(video_idx);
            setPlayingDefault(false);
        });
    });
    console.log(videoIdxQueue);
    return (
        <div className="App">
            <ReactPlayer
                key={counter}
                height={"700px"}
                playing
                url={[
                    {src: `video${videoIdxQueue[0] ?? 0}.webm`, type: 'video/webm'},
                ]}
                onEnded={() => {
                    console.log('ended');
                    if (!playingDefault) {
                        videoIdxQueue.splice(0, 1);
                    }
                    setPlayingDefault(videoIdxQueue.length === 0);
                    setCounter(counter + 1);
                }}
            />
        </div>
    );
}

export default App;
