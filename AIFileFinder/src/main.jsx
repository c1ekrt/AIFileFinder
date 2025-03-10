import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css'

import App from './App.jsx'
import FolderInput from './FolderInput.jsx'
import FileFinder from './FileFinder.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route index path="/main" element={<><App /><FolderInput /></>}/>
        <Route path="/finder" element={<FileFinder />}/>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
