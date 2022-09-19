import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import styled from "styled-components";

//Router
import LandingPage from "./routes/LandingPage";
import MainPage from "./routes/MainPage";
import SelectPage from "./routes/SelectPage";
import ResultPage from "./routes/ResultPage";

const Wrapper = styled.div`
  width: 99vw;
  height: 85vh;
`;

const defaultData = [
  {
    id: 0,
    className: "",
    roomRelation: "",
  },
  {
    id: 1,
    className: "",
    roomRelation: "",
  },
  {
    id: 2,
    className: "",
    roomRelation: "",
  },
  {
    id: 3,
    className: "",
    roomRelation: "",
  },
  {
    id: 4,
    className: "",
    roomRelation: "",
  },
  {
    id: 5,
    className: "",
    roomRelation: "",
  },
];

function App() {
  // 랜더링 될 20개 dataList
  const [dataList, setDataList] = useState([]);
  // 최종 데이터 도면 name
  const [resultData, setResultData] = useState("");

  return (
    <Wrapper>
      <Router>
        <Routes>
          <Route index element={<LandingPage />} />
          <Route path="/" element={<LandingPage />} />
          <Route
            path="/main"
            element={<MainPage handleDataList={setDataList} />}
          />
          <Route
            path="/select"
            element={
              <SelectPage
                dataList={dataList}
                handleResultData={setResultData}
              />
            }
          />
          <Route
            path="/result"
            element={<ResultPage resultData={resultData || "18-235-1"} />}
          />
        </Routes>
      </Router>
    </Wrapper>
  );
}

export default App;
