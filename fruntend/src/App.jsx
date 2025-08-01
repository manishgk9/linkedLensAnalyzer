import React from "react";
import AnalyezedRespose from "./AnalyzedResponse";
import HomeScreen from "./HomeScreen";
import { useSelector } from "react-redux";
const App = () => {
  const apislice = useSelector((state) => state.storerd);

  // return <AnalyzedResponse data={resumeData} />;
  function get_currect_response_page() {
    if (apislice.state_linkedin) {
      return <AnalyezedRespose />;
    } else if (apislice.state_resume) {
      return <AnalyezedRespose />;
    } else {
      return <HomeScreen />;
    }
  }

  return get_currect_response_page();
};
export default App;
