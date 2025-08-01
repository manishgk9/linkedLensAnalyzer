import React, { use, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { linkedinAnalyze, uploadResume } from "./services/api_handler";
const HomeScreen = () => {
  const apislice = useSelector((state) => state.storerd);
  //   console.log(apislice);
  const [linkedinUsername, setLinkedinUsername] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const dispatch = useDispatch();

  const handleLinkedinSubmit = (e) => {
    e.preventDefault();
    if (linkedinUsername) {
      dispatch(linkedinAnalyze(linkedinUsername));
      console.log(apislice);
      console.log("LinkedIn Username:", linkedinUsername);
    }
  };

  const handlePdfSubmit = (e) => {
    e.preventDefault();
    if (pdfFile) {
      const formData = new FormData();
      formData.append("file", pdfFile);
      dispatch(uploadResume(formData));
      console.log("PDF File:", pdfFile);
    }
  };

  return (
    <div className="min-h-screen bg-[#e6e9f0] font-['Roboto'] flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-[1200px] bg-white rounded-xl shadow-xl overflow-hidden">
        {/* Header */}
        <div className="text-center bg-[#004d9c] text-white py-12 px-4">
          <h1 className="text-4xl font-bold mb-2">Linkedlence Analyzer</h1>
          <p className="text-lg font-light">
            Utilizing Generative AI for smarter insights, suggestions, and
            improvements.
          </p>
        </div>

        {/* Content */}
        <div className="flex flex-col md:flex-row">
          {/* LinkedIn Analyzer */}
          <div className="flex-1 bg-[#f7f9fc] px-10 py-10 border-b md:border-b-0 md:border-r border-gray-300">
            <h2 className="text-2xl font-semibold text-[#004d9c] mb-4">
              🔗 LinkedIn Analyzer
            </h2>
            <p className="text-gray-600 text-base mb-6">
              Analyze a LinkedIn user's profile and posts. Our generative AI
              will provide insights into their content strategy, engagement, and
              offer suggestions for improvement.
            </p>

            <form onSubmit={handleLinkedinSubmit}>
              <div className="mb-4">
                <label
                  htmlFor="linkedin-username"
                  className="block text-gray-700 font-medium mb-2"
                >
                  LinkedIn Username
                </label>
                <input
                  type="text"
                  id="linkedin-username"
                  className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#004d9c]"
                  placeholder="e.g., johndoe"
                  value={linkedinUsername}
                  onChange={(e) => setLinkedinUsername(e.target.value)}
                  required
                />
              </div>
              {apislice.loading_linkedin ? (
                <button
                  type="submit"
                  disabled
                  className="w-full bg-[#014589] hover:bg-[#003366] text-white py-3 rounded-md font-semibold transition-all"
                >
                  Loading profile please wait...
                </button>
              ) : (
                <button
                  type="submit"
                  className="w-full bg-[#004d9c] hover:bg-[#003366] text-white py-3 rounded-md font-semibold transition-all"
                >
                  Analyze LinkedIn
                </button>
              )}
            </form>
          </div>

          {/* PDF Resume Analyzer */}
          <div className="flex-1 bg-white px-10 py-10">
            <h2 className="text-2xl font-semibold text-green-700 mb-4">
              📄 PDF Analyzer
            </h2>
            <p className="text-gray-600 text-base mb-6">
              Upload a PDF document for a comprehensive analysis. Our AI can
              summarize key points, extract important data, and provide
              suggestions for improving the document's structure and clarity.
            </p>

            <form onSubmit={handlePdfSubmit}>
              <div className="mb-4">
                <label
                  htmlFor="pdf-upload"
                  className="block text-gray-700 font-medium mb-2"
                >
                  Upload PDF File
                </label>
                <input
                  type="file"
                  id="pdf-upload"
                  accept=".pdf"
                  onChange={(e) => setPdfFile(e.target.files[0])}
                  className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-600"
                  required
                />
              </div>

              {apislice.loading_resume ? (
                <button
                  type="submit"
                  disabled
                  className="w-full bg-green-800 hover:bg-green-700 text-white py-3 rounded-md font-semibold transition-all"
                >
                  Loading please wait..
                </button>
              ) : (
                <button
                  type="submit"
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-md font-semibold transition-all"
                >
                  Analyze PDF
                </button>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;
