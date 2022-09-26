import axios from "axios";

export const request = async (data) => {
  axios // axios 라고 프론트에서 ajax (비동기요청) 하는 모듈
    // .get(`${config.API_ADDRESS}`) // GET 요청을 API_ADDRESS로 보내겠다.  칵셔너리에서 특정 칵테일 id 를 가진 칵테일 불러오는 API 예시: config.API_ADDRESS + "/cocktionary/{cocktail_id}"
    .get(`http://43.200.182.192:8080`, {
      params: { data: JSON.stringify(data) },
    })
    .then((response) => {
      // console.log(response.status);
      return response.data;
    })
    .catch((e) => {
      // 요청보내놓고 에러를 캐치하는곳
      // console.log(e.response.data);
      alert("예기치 못한 에러가 발생했습니다.");
    });
};
