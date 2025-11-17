import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useFormik } from "formik";
import * as yup from "yup";
import { FiEye, FiEyeOff } from "react-icons/fi";

function Authentication({ updateUser }) {
  const [activeTab, setActiveTab] = useState("login");
  const [errorMessage, setErrorMessage] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const navigate = useNavigate();

  const loginSchema = yup.object().shape({
    username: yup.string().required("Please enter a username"),
    password: yup.string().required("Please enter a password"),
  });

  const signupSchema = yup.object().shape({
    username: yup.string().required("Please enter a username"),
    password: yup.string().required("Please enter a password"),
    email: yup.string().email("Invalid email address").required("Please enter an email"),
  });

  const formik = useFormik({
    initialValues: {
      username: "",
      password: "",
      email: "",
    },
    validationSchema: activeTab === "signup" ? signupSchema : loginSchema,
    onSubmit: (values) => {
      fetch(activeTab === "signup" ? "/api/signup" : "/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      })
        .then((res) => {
          if (res.ok) {
            res.json().then((user) => {
              updateUser(user);
              navigate("/");
            })
          } else {
            res.json().then(res => setErrorMessage(res.error));
          }
        });
    },
    validateOnChange: false,
    validateOnBlur: false,
  });

  const handleTabSwitch = (tab) => {
    setActiveTab(tab);
    setErrorMessage(null);
    formik.resetForm();
  }


  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="bg-white rounded-xl shadow-lg max-w-md w-full p-8">
        <div className="flex justify-center mb-6 border-b border-gray-200">
          <button
            onClick={() => handleTabSwitch("login")}
            className={`px-4 py-2 font-medium ${
              activeTab === "login" ? "border-b-2 border-[#FF7E6B]" : "text-gray-500"
            } transition-colors`}
          >
            Login
          </button>

          <button
            onClick={() => handleTabSwitch("signup")}
            className={`px-4 py-2 font-medium ${
              activeTab === "signup" ? "border-b-2 border-[#FF7E6B] text-[#FF7E6B]" : "text-gray-500"
            } transition-colors`}
          >
            Sign Up
          </button>
        </div>

        {errorMessage && <p className="text-red-500 text-sm mb-2">{errorMessage}</p>}
        {formik.errors &&
          Object.values(formik.errors).map((error, index) => (
            <p key={index} className="text-red-500 text-sm mb-2">
              {error}
            </p>
        ))}

        <form onSubmit={formik.handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              name="username"
              value={formik.values.username}
              onChange={formik.handleChange}
              placeholder="Enter username"
              className="w-full px-2 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#86ABBD] text-gray-800"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                value={formik.values.password}
                onChange={formik.handleChange}
                placeholder="Enter password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#86ABBD] text-gray-800"
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                {showPassword ? <FiEye size={18} /> : <FiEyeOff size={18} />}
              </button>
            </div>
          </div>

          {activeTab === "signup" && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formik.values.email}
                onChange={formik.handleChange}
                placeholder="Enter email"
                className="w-full px-2 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#83ABBD] text-gray-800"
              />
            </div>
          )}

          <button 
            type="submit"
            className="w-full py-2 rounded-lg bg-[#FF7E6B] text-white font-semibold hover:bg-[#E56253] transition-colors duration-200"
          >
            {activeTab === "signup" ? "Sign up" : "Log in"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Authentication;
