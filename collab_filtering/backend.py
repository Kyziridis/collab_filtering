import matplotlib.pyplot as plt

from collab_filtering.api_objects import RequestInputData


# Please add the gunzip file under the data directory.
SIMILARITY_THRESSHOLD = 0.5


class DataManager:
    """
    Class for handling the incoming data streams.
     - Incremental Item-to-Item collaborating filtering.
     - For each mediaId which is consumed (<streamend>), apply collaborating filtering.
     - Recomment all similar items for the current target item based on threshold.
     - Method run is the main function which calls all the others.
    """

    def __init__(self) -> None:
        self.item_users = {}
        self.user_items = {}
        self.items_consumed = {}
        self.users_freq = {}
        self.sims = {}
        self.n_api_hits = 0
        self.response = {'most_popular': None,
                         'recommendation_sim_items': None}

    def run(self, input_stream: RequestInputData) -> None:
        """
        Function for running the full flow.
         - Handles the incoming streams.
         - Update the toy_example "data_base": item_user, user_item, sims
         - Runs the collaborating filtering if it is feasible.
        """
        self.n_api_hits += 1
        response = self.response
        if input_stream.EventType.value == 'streamend':
            self._update(input_stream)
            similar_items = self._recommend(input_stream)
            response['most_popular'] = max(
                self.items_consumed, key=self.items_consumed.get) if self.items_consumed else None
            response['recommendation_sim_items'] = {
                input_stream.MediaId: similar_items}
        return response

    def report_statistics(self, plot=False) -> tuple[dict]:
        users = dict(sorted(self.users_freq.items(),
                     key=lambda x: x[1], reverse=True)[:5])
        items = dict(sorted(self.items_consumed.items(),
                     key=lambda x: x[1], reverse=True)[:5])

        if plot:
            self._bar(users, "Top_5_users")
            self._bar(items, "Top_5_items")
        return users, items

    def _recommend(self, input_stream: RequestInputData):
        """
        Function for the actual collaborating filtering. 
        Recommendation is made based on the jaccard similarity.
        """

        target_item = input_stream.MediaId
        if not len(self.user_items[input_stream.UserId][:-1]):
            for sim_item in self.sims[target_item]:
                score = self._jaccard_sim(set(self.item_users[target_item]),
                                          set(self.item_users[sim_item]))
                self._update_sims(target_item, sim_item, score)
            return self.sims[target_item]

        for item in self.user_items[input_stream.UserId][:-1]:
            score = self._jaccard_sim(set(self.item_users[target_item]),
                                      set(self.item_users[item]))
            self._update_sims(target_item, item, score)

        for sim_item in self.sims[target_item]:
            score = self._jaccard_sim(set(self.item_users[target_item]),
                                      set(self.item_users[sim_item]))
            self._update_sims(target_item, sim_item, score)

        return self.sims[target_item]

    def _update_sims(self,
                     target_item: int,
                     item: int,
                     score: float):
        """
        Update similarities based on thresshold
        """

        if score >= SIMILARITY_THRESSHOLD:
            if target_item not in self.sims[item]:
                self.sims[item].append(target_item)
            if item not in self.sims[target_item]:
                self.sims[target_item].append(item)
        else:
            if target_item in self.sims[item]:
                self.sims[item].remove(target_item)
            if item in self.sims[target_item]:
                self.sims[target_item].remove(item)

    def _update(self, input_stream: RequestInputData):
        """
        Update step for:
          item_user/user_item
          current similarities
          all items that have been consumed
        """

        if input_stream.MediaId not in self.item_users:
            self.item_users[input_stream.MediaId] = [input_stream.UserId]
            self.items_consumed[input_stream.MediaId] = 1
            self.sims[input_stream.MediaId] = []
        else:
            if input_stream.UserId not in self.item_users[input_stream.MediaId]:
                self.item_users[input_stream.MediaId].append(
                    input_stream.UserId)
                self.items_consumed[input_stream.MediaId] += 1

        if input_stream.UserId not in self.user_items:
            self.user_items[input_stream.UserId] = [input_stream.MediaId]
            self.users_freq[input_stream.UserId] = 1
        else:
            if input_stream.MediaId not in self.user_items[input_stream.UserId]:
                self.user_items[input_stream.UserId].append(
                    input_stream.MediaId)
                self.users_freq[input_stream.UserId] += 1

    def _jaccard_sim(self, set_a: set, set_b: set):
        if len(set_a.union(set_b)) > 0:
            return len(set_a.intersection(set_b))/len(set_a.union(set_b))
        return 0

    def _bar(self, y: dict, title: str):
        objects = y.keys()
        freq = y.values()
        y_pos = [i for i in range(len(objects))]

        plt.bar(y_pos, freq, align='center', alpha=0.5)
        plt.xticks(y_pos, objects)
        plt.ylabel("Frequency")
        plt.title(title)
        plt.savefig(f"exports/{title}.png")
        plt.close()
