
const Loading = ({ message = "Loading..." }) => {
  return (
    <div className="flex justify-center items-center h-full p-6">
      <div className="text-center text-gray-600">
        <p className="text-lg font-medium">{message}</p>
        <div className="mt-2 animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
      </div>
    </div>
  );
};

export default Loading;
