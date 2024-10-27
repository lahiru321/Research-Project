import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../components/sociel.css';
import prod1Image from '../products/prod1.png';
const Social = () => {
    const [data, setData] = useState({ positive: 0, negative: 0, reviews: [] });
    const [text, setText] = useState("");

    useEffect(() => {
        // Fetch initial data from backend
        fetch("http://localhost:8000/data")
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        
        // Send text input to backend
        const response = await fetch("http://localhost:8000/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        if (result.message === "Text processed successfully") {
            // Fetch updated data
            fetch("http://localhost:8000/data")
                .then(response => response.json())
                .then(data => setData(data))
                .catch(error => console.error("Error updating data:", error));
        }
        setText("");  // Clear the input
    };

    return (
        <div>
            <div className="split left">
                <div className="centered">
                <a href="https://vrch.at/r3v63gx4" target="_blank" rel="noopener noreferrer"><img src={prod1Image} alt="join vr" />
                 </a> 
                </div>
            </div>

            <div className="split right">
                <div className="container mt-5 mb-5">
                    <div className="d-flex justify-content-center row">
                        <div className="d-flex flex-column col-md-8">
                            <div>
                                <label>Positive Experience: {data.positive}</label>
                            </div>
                            <div>
                                <label>Negative Experience: {data.negative}</label>
                            </div>
                            <div>
                                <form onSubmit={handleSubmit}>
                                    <textarea value={text} onChange={(e) => setText(e.target.value)} />
                                    <input type="submit" />
                                </form>
                            </div>

                            <div className="coment-bottom bg-white p-2 px-4">
                                {data.reviews.map((review, index) => (
                                    <React.Fragment key={index}>
                                        <hr />
                                        <div className="commented-section mt-2">
                                            <div className="text-nowrap bd-highlight">
                                                <span>{review}</span>
                                            </div>
                                            <hr />
                                        </div>
                                    </React.Fragment>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Social;
