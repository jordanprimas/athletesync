import React from 'react'
import { Link } from 'react-router-dom'
import UserPostList from '../posts/UserPostList'


const Home = ({ user, posts, handleEditClick, handleDeleteClick }) => {

  const userPosts = posts.filter(post => post.user_id === user.id)
  
  return (
    <div className="min-h-screen bg-[##F8FAFC] py-10 px-4">
      {/* Page Header - create new posts button */}
      <div className="max-w-6xl mx-auto mb-8 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-800">My Posts</h2>
        <Link 
          to={`/posts/new`} 
          className="bg-[#FF7E6B] text-white px-4 py-2 rounded-lg 
          shadow-md hover:bg-[#E56253] transition-all duration-200"
        >
          Create Post
        </Link>
      </div>

      {/* Posts grid */}
      <UserPostList postList={userPosts} handleEditClick={handleEditClick} handleDeleteClick={handleDeleteClick} />
    </div>
  )
}

export default Home