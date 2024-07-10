import Cookies from "universal-cookie";

const cookies = new Cookies();
var email = "";
export const getToken = () => {
    const token = cookies.get('token');
    return token;
};
  
export const getUserEmail = () => {
    const userEmail = cookies.get('userEmail');
    email = userEmail;
    return userEmail;
};


export const deleteCookie = () => {
    cookies.remove('token');
    cookies.remove('userEmail');
};

