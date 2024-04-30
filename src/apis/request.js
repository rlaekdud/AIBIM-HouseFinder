import axios from "axios";

export const request = async (data) => {
  return axios // axios 라고 프론트에서 ajax (비동기요청) 하는 모듈
    .get(`http://43.201.14.251:8080`, {
      params: { data: JSON.stringify(data) },
    })
    .then((response) => {
      return response.data;
    })
    .catch((e) => {
      // 요청보내놓고 에러를 캐치하는곳
      // console.log(e.response.data);
      alert("예기치 못한 에러가 발생했습니다.");
    });
};
