import React, { useState } from "react";

export default function AddTransactionModal({
  onClose,
  onAdd,
  mode = "add",
  transaction = null,
}) {
  const [formData, setFormData] = useState(() => {
    return transaction
      ? {
          ...transaction,
          amount: transaction.amount.toString(),
          date: transaction.date,
          payment_method: transaction.payment_method
            ?.toLowerCase()
            .replace(" ", "_"),
        }
      : {
          transaction_type: "expense",
          item_name: "",
          shop_name: "",
          amount: "",
          date: "",
          payment_method: "cash",
          category: "Housing",
          user: 1,
        };
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      amount: parseFloat(formData.amount),
      date: new Date(formData.date).toISOString().split("T")[0],
      payment_method: formData.payment_method.toLowerCase().replace(" ", "_"),
    };

    const url =
      mode === "edit"
        ? `http://localhost:8000/api/transactions/${transaction.id}/`
        : "http://localhost:8000/api/transactions/";

    const method = mode === "edit" ? "PATCH" : "POST";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        onAdd(data);
        onClose();
      })
      .catch((err) => console.error("Error saving transaction:", err));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-md p-6 rounded shadow-lg relative">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-lg"
        >
          &times;
        </button>
        <h2 className="text-lg font-semibold mb-4">Add New Transaction</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 font-medium">Transaction Type</label>
            <select
              name="transaction_type"
              value={formData.transaction_type}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            >
              <option value="expense">Expense</option>
              <option value="revenue">Revenue</option>
            </select>
          </div>
          <div>
            <label className="block mb-1 font-medium">Item Name</label>
            <input
              name="item_name"
              value={formData.item_name}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Shop Name</label>
            <input
              name="shop_name"
              value={formData.shop_name}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Amount</label>
            <input
              name="amount"
              type="number"
              step="0.01"
              value={formData.amount}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Date</label>
            <input
              name="date"
              type="date"
              value={formData.date}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-medium">Payment Method</label>
            <select
              name="payment_method"
              value={formData.payment_method}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            >
              <option value="Cash">Cash</option>
              <option value="Credit Card">Credit Card</option>
              <option value="Debit Card">Debit Card</option>
              <option value="Bank Transfer">Bank Transfer</option>
              <option value="Mobile Payment">Mobile Payment</option>
            </select>
          </div>
          <div>
            <label className="block mb-1 font-medium">Category</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full border px-3 py-2 rounded"
              required
            >
              <option value="Housing">Housing</option>
              <option value="Food">Food</option>
              <option value="Transportation">Transportation</option>
              <option value="Entertainment">Entertainment</option>
              <option value="Shopping">Shopping</option>
              <option value="Others">Others</option>
            </select>
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border rounded text-gray-600 hover:bg-gray-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Done
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
