import { StrictMode, useState, useEffect} from 'react'
import { use, Suspense } from "react";
import { createRoot } from 'react-dom/client'
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { useNavigate } from "react-router-dom";


function FileFinder(){
  const [data, setData] = useState("請描述你要找的檔案");
  const url = "http://127.0.0.1:5000/finder";
    async function onSubmit(e){
      // 點擊觸發API
      e.preventDefault();
      const form = e.target;
      let formData = new FormData();
      const prompt = form.prompt.value
      formData.append("prompt", prompt)
      console.log(input)
      setData(input["prompt"])
    }

    async function sendFormData(formData){
      
      let response = await fetch(url, {
          method: 'POST',
          body: formData
        }).then((response) => response.json());
      console.log(response)

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
          <h3> {data} </h3>
        </div>
        <div>
          <li>

          </li>
        </div>
      </div>
      
    )
}
export default FileFinder;
