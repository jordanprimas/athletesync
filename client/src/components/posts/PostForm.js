import React from 'react'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import * as yup from 'yup'
import { Formik, useFormikContext } from "formik";

const ErrorMessage = ({ name }) => {
  const { errors, touched } = useFormikContext()
  return touched[name] && errors[name] ? (
    <div className="error">{errors[name]}</div>
  ) : null
}

const PostForm = ({ addPost }) => {
  const navigate = useNavigate()


  const initialValues = {
    title: "",
    content: ""
  }

  const formSchema = yup.object().shape({
    title: yup.string().min(1).required("Please enter at least 1 character"),
    content: yup.string().min(10).required("Please enter at least 10 characters"),
  })

  const handleSubmit = (values, { resetForm }) => {
    fetch("/api/posts", {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify(values)
    })
    .then(res => res.json())
    .then(data => {
      addPost(data)
      resetForm()
      navigate("/")
    })
  }

  return (
    <div className="bg-[#3D7E9F] rounded-xl border border-[#E2EF8F] 
      p-6 shadow-md w-full max-w-xl mx-auto my-10"
    >
      <h3 className="text-2xl font-semibold text-white mb-4">✨ Create a new post</h3>
      <p className="text-[#E2EF8F] text-sm mb-4">
        Share your thoughts or something that made your day!
      </p>
      <Formik
        initialValues={initialValues}
        validationSchema={formSchema}
        onSubmit={handleSubmit}
      >
        {formik => (
          <form onSubmit={formik.handleSubmit} className="space-y-5">

            {/* Title Field */}
            <div className="text-red-400">
              <label className="block text-sm text-white font-medium mb-1">Title</label>
              <input 
                type='text'
                name='title'
                value={formik.values.title} 
                placeholder='Enter post title'
                onChange={formik.handleChange}  
                className="w-full rounded-lg border border-gray-300 p-2 text-gray-800
                focus:ring-2 focus:ring-[#86ABBD] outline-none"     
              />
              <ErrorMessage name="title" componenet="p" />
            </div>

            {/* Content Field */}
            <div className="text-red-400">
              <label className="block text-sm text-white font-medium mb-1">Content</label>
              <textarea 
                name='content'
                value={formik.values.content} 
                placeholder='Write post' 
                onChange={formik.handleChange}  
                className='w-full rounded-lg border border-gray-300 p-2 text-gray-800
                focus:ring-2 focus:ring-[#86ABBD] outline-none h-28 resize-none'             
              />
              <ErrorMessage name="content" />
            </div>

            {/* Buttons */}
            <div className="flex justify-end gap-3">
              <Link 
                to="/"
                className="px-4 py-2 rounded-lg bg-white text-[#3D7E9F] font-medium hover:bg-[#F1F5F9] transition-all"
              >
                Cancel
              </Link>
              <button 
                type="submit" 
                className="px-4 py-2 rounded-lg bg-[#FF7E6B] text-white font-semibold
                hover:bg-[#E56253] active:bg-[#CC4d42] transition-all duration-200
                focus:outline-none focus:ring-2 focus:ring-[#FBAFA4]"
              >
                Create Post
              </button>
            </div>
          </form>
        )}
      </Formik>
    </div>
  )
}

export default PostForm
