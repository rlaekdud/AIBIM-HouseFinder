import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import styled from "styled-components";
import { GlobalStyle } from "./GlobalStyles.js";
import { MantineProvider } from "@mantine/core";

//Router
import LandingPage from "./page/LandingPage";
import MainPage from "./page/MainPage";
import SelectPage from "./page/SelectPage";
import ResultPage from "./page/ResultPage";

const Wrapper = styled.div`
  width: 99vw;
  height: 85vh;
`;

function App() {
  // 랜더링 될 20개 dataList
  const [dataList, setDataList] = useState([]);
  // 최종 데이터 도면 name, string 으로 저장
  const [resultData, setResultData] = useState([]);

  return (
    <Wrapper>
      <MantineProvider
        theme={{
          fontFamily: "SCoreDream",
          fontWeight: "500",
        }}
      >
        <GlobalStyle />
        <Router>
          <Routes>
            <Route index element={<LandingPage />} />
            <Route path="/" element={<LandingPage />} />
            <Route
              path="/main"
              element={
                <MainPage dataList={dataList} handleDataList={setDataList} />
              }
            />
            <Route
              path="/select"
              element={
                <SelectPage
                  dataList={dataList}
                  handleDataList={setDataList}
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
      </MantineProvider>
    </Wrapper>
  );
}

export default App;
