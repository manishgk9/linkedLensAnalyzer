// api call for getting post req
import { createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// thunk
const BASE_URL = "http://localhost:8000";
export const linkedinAnalyze = createAsyncThunk(
  "/linkedin-analyze",
  async (formData, thunkAPI) => {
    formData = {
      username: formData,
    };
    try {
      const response = await axios.post(
        `${BASE_URL}/analyze-linkedin`,
        formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || error.message);
    }
  }
);

// linkedin analyze
export const uploadResume = createAsyncThunk(
  "/upload-test-resume",
  async (formData, thunkAPI) => {
    try {
      const response = await axios.post(`${BASE_URL}/upload-resume`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      return response.data;
    } catch (error) {
      return thunkAPI.rejectWithValue(error.response?.data || error.message);
    }
  }
);
