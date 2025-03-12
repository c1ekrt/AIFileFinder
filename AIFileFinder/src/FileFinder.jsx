import { StrictMode, useState, useEffect} from 'react'
import { use, Suspense } from "react";
import { createRoot } from 'react-dom/client'
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import { useNavigate } from "react-router-dom";


function FileFinder(){
  const [data, setData] = useState("請描述你要找的檔案");
    async function onSubmit(e){
      // 點擊觸發API
      const url = "http://127.0.0.1:5000/finder"
      let response = await fetch(url)
                .then((response) => response.json());
      e.preventDefault();
      const form = e.target;
      const formData = new FormData(form);
      const input = Object.fromEntries(formData.entries())
      console.log(input)
      setData(input["prompt"])
    }


    return(
      <div>
        <div>
          <form method="get" onSubmit={onSubmit}>
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
