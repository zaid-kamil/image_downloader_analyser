from imageai.Prediction import ImagePrediction
import os


def makeprediction(path):
	if os.path.exists(path):
		try:
			prediction = ImagePrediction()
			prediction.setModelTypeAsResNet()
			prediction.setModelPath("resnet50_weights_tf_dim_ordering_tf_kernels.h5")
			prediction.loadModel()

			# fullpath = os.path.join(execution_path, path)
			print(path)
			predictions, probabilities = prediction.predictImage(path, result_count=3)
			for eachPrediction, eachProbability in zip(predictions, probabilities):
				print(eachPrediction, " : ", eachProbability)
				return eachPrediction,eachProbability
		except Exception as e:
			print(e)
	return None,None
    


if __name__ == '__main__':
    print(makeprediction('download/img.jpg'))