import './FolderInput.css'

export default function FolderInput(){
    function HandleSubmit(e){
        // Prevent the browser from reloading the page
        e.preventDefault();
        // Read the form data
        const form = e.target;
        const formData = new FormData(form);
        
        // You can work with it as a plain object:
        const formJson = Object.fromEntries(formData.entries());
    }
    return(
        <div>
            <form method="post" onSubmit={HandleSubmit}>
                <label>
                    Folder Path: <input name="folder_path" defaultValue="D:\\" />
                </label>
                <hr />
                <button type="submit">Submit</button>
            </form>
        </div>

    );
}
