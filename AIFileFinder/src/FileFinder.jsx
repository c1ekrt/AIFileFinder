import { StrictMode, useState, useEffect} from 'react'
import { use, Suspense } from "react";
import { createRoot } from 'react-dom/client'
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { useNavigate } from "react-router-dom";


export default function FileFinder(){
  const [data, setData] = useState("請描述你要找的檔案");
  const [response, setResponse] = useState(["檔案"]);
  const listItems = response.map(item =>
    <li>{item}</li>
  );
  const url = "http://127.0.0.1:5000/finder";
    async function onSubmit(e){

      e.preventDefault();
      const form = e.target;
      let formData = new FormData();
      const prompt = form.prompt.value
      console.log(prompt)
      formData.append("prompt", prompt)
      setData(prompt)
      let file = await sendFormData(formData)
      console.log(file)
      setResponse(file)
    }

    async function sendFormData(formData){
      
      let response = await fetch(url, {
        method: 'POST', 
        body: formData
      }).then((response) => response.json());
      console.log(response)
        return response["response"]
    }

    return(
      <div>
        <div>
          <form method="post" onSubmit={onSubmit}>
              <label>
                  File Description: <input name="prompt" defaultValue="請描述你要找的檔案"/>
              </label>
              <hr />
              
              <button type="submit" >Submit</button>
          </form>
          <hr />
          <h3> 正在查找 {data} 相關的資料 </h3>
        </div>
        <div>
          <ul>{listItems}</ul>;
        </div>
      </div>
      
    )
}
