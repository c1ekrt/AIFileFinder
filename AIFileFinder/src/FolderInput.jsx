import './FolderInput.css'
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
// https://stackoverflow.com/questions/75649339/sending-form-data-from-react-to-flask-server
export default function FolderInput(){
    let navigate = useNavigate();
    let input = ''
    async function HandleSubmit(e){
        e.preventDefault();
        const form = e.target;
        const path = form.path.value

        let formData = new FormData();
        formData.append('path', path)
        await sendFormData(formData)

    }

    async function sendFormData(formData){
        const url = "http://127.0.0.1:5000/";
        let response = await fetch(url, {
            method: 'POST',
            body: formData
          }).then((response) => response.json());
        console.log(response)
        navigate("/finder");
    }

    return(
        <div>
            <form method="get" onSubmit={HandleSubmit}>
                <label>
                    Folder Path: <input id="path" name="path" defaultValue="D:\" />
                </label>
                <hr />
                
                <button type="submit" >Submit</button>
            </form>
        </div>

        

    );
}
