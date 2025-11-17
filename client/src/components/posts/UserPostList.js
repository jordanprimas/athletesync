import React from "react"
import UserPostCard from "./UserPostCard"

const UserPostList = ( {postList, handleEditClick, handleDeleteClick} ) => {
    
    const userPostElementList = postList.map(post => (
        <UserPostCard key={post.id} post={post} handleEditClick={handleEditClick} handleDeleteClick={handleDeleteClick} />
    ))

  return (
    // Current user's card grid
    <div className="max-w-6xl mx-auto grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {userPostElementList}
    </div>
  )
}

export default UserPostList