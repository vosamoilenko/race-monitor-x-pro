import { initializeApp } from 'firebase/app'
import { getFirestore, collection, getDocs, doc } from 'firebase/firestore'
import { useCollection, useDocument } from 'vuefire'

export const useFirestore = () => {
  const firebaseApp = initializeApp({
    apiKey: import.meta.env.VITE_API_KEY,
    authDomain: import.meta.env.VITE_AUTH_DOMAIN,
    databaseURL: import.meta.env.VITE_DATABASE_URL,
    projectId: import.meta.env.VITE_PROJECT_ID,
    storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
    messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
    appId: import.meta.env.VITE_APP_ID,
    measurementId: import.meta.env.VITE_MEASUREMENT_ID
  })

  const db = getFirestore(firebaseApp)

  const col = () => {
    return useCollection(collection(db, 'data'))
  }
  const doc1 = () => {
    return useDocument(doc(db, 'data', 'vova'))
  }

  // Function to get all document IDs from the 'data' collection
  const getAllDocumentIds = async () => {
    try {
      const dataCollection = collection(db, 'data')
      const snapshot = await getDocs(dataCollection)
      const documentIds = snapshot.docs.map((doc) => doc.id)
      console.log('Document IDs:', documentIds)
      return documentIds
    } catch (error) {
      console.error('Error getting document IDs:', error)
      throw error
    }
  }

  const getDocument = (id: string) => {
    try {
      const docRef = doc(db, 'data', id)
      return docRef
    } catch (error) {
      console.error('Cannot get document', error)
      throw error
    }
  }

  return { getAllDocumentIds, getDocument, col, doc1 }
}
