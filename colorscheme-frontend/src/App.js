import {useState} from 'react'
import './App.scss';

function App() {
  const [preview,setPreview] = useState()
  const [theme, setTheme] = useState({"colors":[],"dark":[]})
  function handleFileInput(e) {
    console.log(e.target.files[0])
    if(e.target.files[0]) setPreview(URL.createObjectURL(e.target.files[0]));
  }

  async function getScheme() {
    const formData = new FormData();
    formData.append('file', document.getElementById("fileinput").files[0]);
    const options = {
      method: 'POST',
      body: formData,
      // If you add this, upload won't work
      // headers: {
      //   'Content-Type': 'multipart/form-data',
      // }
    };
    
    document.getElementById("loading").style.display = "flex";
    let response = await fetch('http://localhost:5000/upload', options)
    if(response.ok) {
      let json = await response.json()
      setTheme(json)
    } else {
      console.error("something went wrong")
    }
    document.getElementById("loading").style.display = "none";
  }

  return (
    <div className="app">
      <div id="loading"><img src="https://c.tenor.com/5o2p0tH5LFQAAAAi/hug.gif"/></div>
      <div className="block upload">
        <input id="fileinput" onInput={handleFileInput} type="file"/>
        <button onClick={getScheme}>Get Scheme</button>
      </div>
      <div className="block preview">
        <img src={preview}/>
      </div>
      <div className="block theme">
        {
          Object.keys(theme).map(key => 
            
          <div className={"colors "+key}>
            {
              theme[key].map(hex => <span style={{backgroundColor:hex}}>{hex}</span>)
            }
          </div>
        )
        }
      </div>
    </div>
  );
}

export default App;
