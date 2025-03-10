import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';

function FileFinder(){
    const onSearch = () => {
        navigate(`/search?q=${searchedText}`);
        fetch('/main',{
          method: 'POST',
          body: JSON.stringify({
            content:searchedText
          })
        }).then(response => response.json().then(data => ({ data, response }))).then(({ data, response }) =>  {
          console.log(data)
        });
    }
    return(
      <div>
        <h1>FileFinder</h1>
      </div>
    )
}
export default FileFinder;
