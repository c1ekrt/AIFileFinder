import './FolderInput.css'
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
// https://stackoverflow.com/questions/75649339/sending-form-data-from-react-to-flask-server
export default function FolderInput(){
    let [filecount, setFilecount] = useState(0)
    const [progressbar, setProgressbar] = useState(0)
    const url = "http://127.0.0.1:5000/";
    const file_count_url = "http://127.0.0.1:5000/filecount"  ;
    let navigate = useNavigate();
    async function HandleSubmit(e){
        e.preventDefault();
        const form = e.target;
        const path = form.path.value

        let formData = new FormData();
        formData.append('path', path);
        await sendFileData(formData);
        await sendFormData(formData);

    }

    async function sendFormData(formData){
        let response = await fetch(url, {
            method: 'POST', 
            body: formData
          }).then((response) => response.json());
        console.log(response)
        navigate("/finder");
        
    }

    async function sendFileData(formData){
        let response = await fetch(file_count_url, {
            method: 'POST',
            body: formData
        }).then((response) => response.json());
        console.log(response)
        setFilecount(response["filecount"])
        setProgressbar(null)
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
            <div id="Progress_Status">
            <div id="myprogressBar"></div>
            </div>
            <h3>偵測到 {filecount} 個檔案 </h3>
            <h3>每個檔案的處理時間約為 2 秒</h3>
            <h3>預估處理時間為 {Math.floor((filecount * 2 + 10) / 60)} 分 {(filecount * 2 + 10) % 60} 秒</h3>
            <h3>完成處理後會自動跳轉</h3>
            <div>
                <progress value={progressbar}/>
            </div>
            

        </div>

        

    );
}
