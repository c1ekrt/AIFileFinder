import './FolderInput.css'
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function FolderInput(){
    let navigate = useNavigate();
    async function HandleSubmit(e){
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const formJson = Object.fromEntries(formData.entries());
        console.info(formJson);
        

    }
    async function handleClick (){
        navigate("/finder");
    }

    return(
        <div>
            <form method="post" onSubmit={HandleSubmit}>
                <label>
                    Folder Path: <input name="path" defaultValue="D:\\" />
                </label>
                <hr />
                
                <button type="submit" onClick={handleClick}>Submit</button>
            </form>
            <div>
                <hr />
                <button onClick={handleClick} type="button" value="submit"/>
            </div>
        </div>

        

    );
}
