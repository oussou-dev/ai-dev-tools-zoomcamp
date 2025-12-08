import React from 'react';
import { useNavigate } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';

const Home = () => {
    const navigate = useNavigate();

    const createRoom = () => {
        const roomId = uuidv4();
        navigate(`/room/${roomId}`);
    };

    return (
        <div className="home-container">
            <h1>Code Interview Platform</h1>
            <p>Real-time collaborative coding environment</p>
            <button onClick={createRoom} className="create-btn">
                Create New Interview
            </button>
        </div>
    );
};

export default Home;
