import React, {useEffect, useState} from 'react';
import {io} from "socket.io-client";
import './App.css';
import ReactPlayer from 'react-player';

function App() {

    const [videoIdxQueue] = useState<Array<[number, number]>>([]);
    const [playingDefault, setPlayingDefault] = useState<boolean>(true);
    const [counter, setCounter] = useState<number>(0);

    useEffect(() => {
        const socket = io("http://localhost:5000");
        socket.on('video_queued', ({video_type, video_idx}) => {
            videoIdxQueue.push([video_type, video_idx]);
            setPlayingDefault(false);
        });
    }, []);
    const [a, b] = videoIdxQueue[0] ?? [0, 0];
    return (
        <div className="App" style={{backgroundColor: "black"}}>
            <ReactPlayer
                key={counter}
                height={"720px"}
                playing
                url={[
                    {src: `${a}/${a}-${b}.mp4`, type: 'video/mp4'},
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
