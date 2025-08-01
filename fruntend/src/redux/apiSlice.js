import { createSlice } from "@reduxjs/toolkit";
import { uploadResume, linkedinAnalyze } from "../services/api_handler";
const apiSlice = createSlice({
  name: "apislice",
  initialState: {
    loading_linkedin: false,
    loading: false,
    gimini_data: null,
    error: "",
    state_linkedin: false,
    state_resume: false,
    loading_resume: false,
  },
  reducers: {
    onback: (state) => {
      state.loading_linkedin = false;
      state.loading = false;
      state.gimini_data = null;
      state.state_linkedin = false;
      state.state_resume = false;
      state.loading_resume = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(linkedinAnalyze.pending, (state) => {
        state.loading = true;
        state.loading_linkedin = true;
        state.error = null;
      })
      .addCase(linkedinAnalyze.rejected, (state, action) => {
        state.loading = false;
        state.loading_linkedin = false;
        state.error = action.payload;
      })
      .addCase(linkedinAnalyze.fulfilled, (state, action) => {
        state.loading = false;
        state.gimini_data = action.payload;
        state.loading_linkedin = false;
        state.error = null;
        state.state_linkedin = true;
      })
      .addCase(uploadResume.pending, (state) => {
        state.loading = true;
        state.loading_resume = true;
        state.error = null;
      })
      .addCase(uploadResume.rejected, (state, action) => {
        state.loading = false;
        state.loading_resume = false;
        state.error = action.payload;
      })
      .addCase(uploadResume.fulfilled, (state, action) => {
        state.loading = false;
        state.loading_resume = false;
        state.gimini_data = action.payload;
        state.error = null;
        state.state_resume = true;
      });
  },
});

export const { onback } = apiSlice.actions;
export default apiSlice.reducer;
