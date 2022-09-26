import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import styled from "styled-components";
import { GlobalStyle } from "./GlobalStyles.js";
import { MantineProvider } from "@mantine/core";
import { defaultDataSet } from "./components/dataSet.js";
import { request } from "./apis/request";

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
  // 임시 선택란 0 ~ 6 번까지 데이터 저장
  const [data, setData] = useState(defaultDataSet);
  // 랜더링 될 20개 dataList -> by surver data render 받음, 객체배열 형태
  const [dataList, setDataList] = useState([]);
  // 최종 데이터 도면 name, string 으로 저장, 객체로 저장할 것
  const [resultData, setResultData] = useState({});

  // kor or eng
  const [dataSet, setDataSet] = useState(true);

  // useEffect(() => {
  //   console.log(dataList);
  // }, [dataList]);

  // method
  const handleReset = () => {
    setDataList([]);
    setResultData({});
    setDataSet(true);
    setData(() => {
      data.map((it) => {
        it.className = "";
        it.roomRelation = "";
      });
      return data;
    });
  };

  const korToNum = (item) => {
    item = item.replaceAll("현관", 0);
    item = item.replaceAll("거실", 1);
    item = item.replaceAll("주방", 3);
    item = item.replaceAll("방", 2);
    item = item.replaceAll("화장실", 4);
    item = item.replaceAll("드레스룸", 5);
    item = item.replaceAll("다용도실", 6);
    item = item.replaceAll("계단실", 7);
    item = item.replaceAll("복도", 8);
    item = item.replaceAll("팬트리실", 9);
    item = item.replaceAll("세탁실", 10);
    item = item.replaceAll("붙박이장", 11);
    item = item.replaceAll("차고지", 19);
    item = item.replaceAll("식당", 20);
    item = item.replaceAll("<->", "_");
    return item;
  };
  const engToNum = (item) => {
    item = item.replaceAll("Hall", 0);
    item = item.replaceAll("Living room", 1);
    item = item.replaceAll("Kichen", 3);
    item = item.replaceAll("Bedroom", 2);
    item = item.replaceAll("Bathroom", 4);
    item = item.replaceAll("Dressing room", 5);
    item = item.replaceAll("Utility room", 6);
    item = item.replaceAll("Stair", 7);
    item = item.replaceAll("Foyer", 8);
    item = item.replaceAll("Pantryroom", 9);
    item = item.replaceAll("Laundry room", 10);
    item = item.replaceAll("Closet", 11);
    item = item.replaceAll("Garage", 19);
    item = item.replaceAll("Dining room", 20);
    item = item.replaceAll("<->", "_");
    return item;
  };

  const handleSubmit = async (items) => {
    const transResult = [];

    // items kor, 영문 판단
    const regex = /^[a-z|A-Z]+$/;
    if (regex.test(items[0][0])) {
      items.map((item) => {
        transResult.push(engToNum(item));
      });
    } else {
      items.map((item) => {
        transResult.push(korToNum(item));
      });
    }
    //console.log(transResult);
    const responseData = await request(transResult);
    // console.log(responseData.data);
    setDataList(responseData.data);
  };

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
                <MainPage
                  data={data}
                  setData={setData}
                  handleReset={handleReset}
                  handleSubmit={handleSubmit}
                  dataSet={dataSet}
                  setDataSet={setDataSet}
                />
              }
            />
            <Route
              path="/select"
              element={
                <SelectPage
                  dataList={dataList}
                  handleReset={handleReset}
                  handleDataList={setDataList}
                  handleResultData={setResultData}
                />
              }
            />
            <Route
              path="/result"
              element={
                <ResultPage language={dataSet} resultData={resultData} />
              }
            />
          </Routes>
        </Router>
      </MantineProvider>
    </Wrapper>
  );
}

export default React.memo(App);
