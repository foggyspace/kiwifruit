import { ConfigProvider } from "antd"
import Router from "./routers";
import {BrowserRouter} from "react-router-dom";

function App() {

  return (
    <>
        <BrowserRouter>
            <ConfigProvider>
                <Router/>
            </ConfigProvider>
        </BrowserRouter>
    </>
  )
}

export default App