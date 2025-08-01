import { configureStore } from "@reduxjs/toolkit";
import apisliceReducer from "./redux/apiSlice";
export const linkdinAndPdfStore = configureStore({
  reducer: {
    storerd: apisliceReducer,
  },
});
