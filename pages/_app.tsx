import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import Cookies from "universal-cookie";
import '@/styles/globals.css';


const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {

  // const [loading, setLoading] = useState<boolean>(true);
  // const [key, setKey] = useState(0);

  // if ((getToken() == null) && (typeof window !== 'undefined'))
  // {
  //   window.location.href = "http://localhost:3000/";
  // }
  
  // console.log("token: " + getToken());
  // console.log("userEmail: " + getCookieEmail());

  // useEffect(() => {
  //   // console.log('Component mounted');
  //   // return () => {
  //     // console.log('Component will be unmount')

  //     //Database: grab user conversations and conversation memory
  //     let data = new URLSearchParams();
  //     data.append("email", getCookieEmail());

  //     let api = "http://219.78.175.160:7000/" + "load-conversations";
  //     fetch(api, { method: "post", body: data })
  //         .then(res => {
  //                 var temp = res.text()
  //                 console.log("res",temp.then(
  //                   data => {
  //                     var messageJson = JSON.parse(data)
  //                     var tempjson = {
  //                       "temp" :  data.toString()
  //                     }
                      
  //                     // For the following json extraction, please refer to console.log(data)
  //                     // console.log("messageJson", messageJson)
  //                     // const number_of_conversations = messageJson['history']['0']['messages']['length']
  //                     // for (var i = 0; i < number_of_conversations; i++) 
  //                     // {
  //                     //   console.log("message", i, messageJson['history']['0']['messages'][i])
  //                     // }
  //                     // console.log("messages",messageJson['history']['0']['messages']['length'])
  //                     // console.log("data",data)
  //                     // console.log("tempjson",tempjson)

  //                     // console.log("test", handleImportConversations(messageJson))
  //                     importData(messageJson);
  //                     setLoading(false);
  //                     // window.location.reload();
  //                   }))
  //               })
  //         .catch(err => console.log(err));

  //   }
  // , []); // notice the empty array here, this is optional

  // useEffect(() => {
  //   setKey(1)
  //   console.log("key", key)
  // }, [loading]);

  const queryClient = new QueryClient();

  // CSS: Loading Component
  // interface LoaderContainerStyles {
  //   width: string;
  //   height: string; 
  //   position: 'fixed' | 'relative' | 'absolute';
  //   background: string;
  //   zIndex: number;
  // }

  // const loaderStyle: LoaderContainerStyles = {
  //   width: '100%',
  //   height: '100vh',
  //   position: 'fixed' as 'fixed',
  //   background: 'rgba(0, 0, 0, 0.834) url("https://media.giphy.com/media/8agqybiK5LW8qrG3vJ/giphy.gif") center no-repeat', 
  //   zIndex: 1  
  // };

  // const spinnerStyle: CSS.Properties = {
  //   width: '64px',
  //   height: '64px', 
  //   border: '8px solid',
  //   borderColor: '#3d5af1 transparent #3d5af1 transparent',
  //   borderRadius: '50%',
  //   animation: 'spin-anim 1.2s linear infinite'
  // };


  // const loaderContainerClass = 'loader-container';
  // const spinnerClass = 'spinner';

  return (
    <div className={inter.className}>
      {/* {loading && <div className={loaderContainerClass}>
        <div className={spinnerClass}></div>
      </div>}
      <div key={key}> */}
        <Toaster />
        <QueryClientProvider client={queryClient}>
          <Component {...pageProps} />
        </QueryClientProvider>
      </div>
    // </div>
  );
}

export default appWithTranslation(App);
