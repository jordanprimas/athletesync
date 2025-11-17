import React, { useState } from 'react';
import * as yup from 'yup';
import { Formik, useFormikContext } from 'formik';
import { FiMoreHorizontal } from "react-icons/fi";
import { GoHeartFill } from "react-icons/go";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import utc from "dayjs/plugin/utc";

dayjs.extend(relativeTime);
dayjs.extend(utc);





const ErrorMessage = ({ name }) => {
  const { errors, touched } = useFormikContext()
  return touched[name] && errors[name] ? (
    <div className="error">{errors[name]}</div>
  ) : null
}

const UserPostCard = ({ post, handleEditClick, handleDeleteClick }) => {
  const [editIsClicked, setEditIsClicked] = useState(false)
  const initialValues = {
    title: post.title,
    content: post.content,
  }
 

  const formSchema = yup.object().shape({
    title: yup.string().min(1, "Your post needs a title!").required('Title is required'),
    content: yup.string().min(10, "Post content should be at least 10 characters").required('Post content should be at least 10 characters'),
  })

  const handleSubmit = (values) => {
    handleEditClick(post.id, values)
    setEditIsClicked(false)
  }



  return (
    <div key={post.id}>

      {/* Edit a post form */}
      {editIsClicked ? (
        <div className="bg-[#3D7E9F] rounded-xl border border-[#E2EF8F0] p-6 shadow-md w-full max-w-xl mx-auto transition-all duration-300">
          <h3 className="text-lg font-semibold text-white pb-3">Edit Post</h3>
          <Formik
            initialValues={initialValues}
            validationSchema={formSchema}
            onSubmit={handleSubmit}
          >
            {formik => (
              <form onSubmit={formik.handleSubmit} className="space-y-5">

                {/* Title Input */}
                <div className='text-red-400'> 
                  <label className="block text-sm text-white font-medium mb-1">Title</label>
                    <input
                      type="text"
                      name="title"
                      value={formik.values.title}
                      placeholder="Enter post title"
                      onChange={formik.handleChange}
                      className="w-full rounded-lg border border-gray-300 p-2 text-gray-800 
                      focus:ring-2 focus:ring-[#86ABBD] outline-none"
                    />
                    <ErrorMessage name="title" component="p" className="text-red-300 !text-red-300 text-sm mt-1" />
                </div>

                {/* Content Input */}
                <div className="text-red-400">
                    <label className="block text-sm text-white font-medium mb-1">Content:</label>
                    <textarea
                      name="content"
                      value={formik.values.content}
                      placeholder="Write your post..."
                      onChange={formik.handleChange}
                      className="w-full rounded-lg border border-gray-300 p-2 text-gray-800 focus:ring-2 focus:ring-[#86ABBD] outline-none h-28 resize-none"
                    />
                    <ErrorMessage name="content" component="p" className="text-red-300 text-sm mt-1" />
                </div>

                {/* Footer Buttons */}
                <div className="flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setEditIsClicked(false)} 
                    className="px-4 py-2 rounded-lg bg-white text-[#3D7E9F] 
                    font-medium hover:bg-[#F1F5F9] transition-all"
                  >
                    Cancel
                  </button> 
                    

                  <button 
                    type="submit" 
                    className="px-4 py-2 rounded-lg bg-[#FF7E6B] text-white 
                    font-semibold hover:bg-[#E56253] active:bg-[#CC4d42] transition-all duration-200
                    focus:outline-none focus:ring-2 focus:ring-[#FBAFA4]"
                  >
                    Save Changes
                  </button>
                </div>
              </form>
            )}
          </Formik>
        </div>
      ) : (

        // Post Card
        <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm max-w-xl w-full mx-auto">
          
          {/* Card Header */}

          <div className="flex items-center justify-between mb-4">
            <div className="w-9 h-9 rounded-full bg-[#86ABBD] text-white flex items-center justify-center font-semibold">
                {post.user.username[0].toUpperCase()}
            </div>
            <div className="flex items-center gap-3 text-sm text-gray-500">
              <p className="font-semibold text-gray-800">{post.user.username}</p>
              <span className="w-1 h-1 bg-gray-400 rounded-full inline-block"></span>
              <span>{dayjs.utc(post.created_at).local().fromNow()}</span>
            </div>

              <FiMoreHorizontal 
              className="w-6 h-5 text-gray-500 cursor-pointer hover:text-gray-700"
              onClick={() => setEditIsClicked(true)} 
              /> 
          </div>
          
          {/* Card Contenet */}
          <div className="bg-[#3d7e9f] space-y-3 text-white rounded-lg p-4 mb-4">
            <h3 className="text-lg font-semibold mb-1">{post.title}</h3>
            <p className="text-sm leading-relaxed">{post.content}</p>
          </div>
            
          {/* Card Footer Buttons */}
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-2" >
              <GoHeartFill className="text-[#FF7E6B] w-5 h-5" /> 
              <span className="text-sm">
                {post.likes.length}
              </span>
            </div>
            <button 
              onClick={() => handleDeleteClick(post.id)}
              className="text-sm text-red-500 hover:text-red-600 transition"
            >
              Delete
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default UserPostCard;
