import React, {useEffect, useState} from 'react';
import {io} from "socket.io-client";
import './App.css';
import ReactPlayer from 'react-player';

const videoConfig = [7, 4, 4, 4, 3, 3, 4];

function App() {

    const [videoIdxQueue] = useState<Array<number>>([]);
    const [playingDefault, setPlayingDefault] = useState<boolean>(true);
    const [counter, setCounter] = useState<number>(0);

    useEffect(() => {
        const socket = io("http://localhost:5000");
        socket.on('video_queued', ({video_type}) => {
            videoIdxQueue.push(video_type);
            setPlayingDefault(false);
        });
    }, []);
    const a = videoIdxQueue[0] ?? 0;
    const b = Math.floor(Math.random() * videoConfig[a]);
    const video = `${a}/${a}-${b}.mp4`;
    console.log(`playing video ${video}`);
    return (
        <div className="App" style={{backgroundColor: "black"}}>
            <ReactPlayer
                key={counter}
                height={"720px"}
                playing
                url={[
                    {src: video, type: 'video/mp4'},
                ]}
                onEnded={() => {
                    console.log('ended');
                    console.log(videoIdxQueue);
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
