<template>
  <div class="tenancy-list-all">
    <h1>All Tenancies</h1>
    <div class="table-container">
      <table class="table tenancy-list">
        <thead>
          <th scope="col">Tenants involved</th>
          <th scope="col">Start Date</th>
          <th scope="col">End Date</th>
          <th scope="col">Property Address</th>
          <th scope="col">Room</th>
          <th scope="col">Rent Cost</th>
          <th scope="col">Next Payment</th>
          <th scope="col">Payment Terms</th>
          <th scope="col">Notes</th>
          <th scope="col">Status</th>
          <th scope="col"></th>
        </thead>
        <tbody>
          <tr v-for="tenancyItem in tenancyList" v-bind:key="tenancyItem.Tenancy.id">
            <td>
              {{ tenancyItem.TenantsNames.join(", ") }}
            </td>
            <td>
              {{ tenancyItem.Tenancy.start_date }}
            </td>
            <td>
              {{ tenancyItem.Tenancy.end_date }}
            </td>
            <td>
              {{ tenancyItem.Tenancy.address }}
            </td>
            <td>
              {{ tenancyItem.Tenancy.room_name }}
            </td>
            <td>
              ${{ tenancyItem.Tenancy.rent_cost }} {{ tenancyItem.PaymentTerms }}
            </td>
            <td>
              {{ tenancyItem.NextPayment }}
            </td>
            <td>
              {{ tenancyItem.PaymentTerms }}
            </td>
            <td>
              {{ tenancyItem.Tenancy.notes }}
            </td>
            <td>
              {{ tenancyItem.TenancyStatus }}
            </td>
            <td>
              <div class="btn">Edit tenancy</div>
            </td>
          </tr>
        </tbody>
        <tfoot></tfoot>
      </table>
    </div>
  </div>
</template>

<script>
import tenancyAPI from '@/_api/tenancy';

export default {
  name: 'tenancy-list-all',
  data() {
    return {
      tenancyList: [],
    };
  },
  mounted() {
    const vm = this;
    vm.$nextTick(() => {
      tenancyAPI.listTenancies((response) => {
        vm.fillTenancyList(response.data);
      }, (error) => {
        console.log(error);
      });
    });
  },
  methods: {
    fillTenancyList(data) {
      this.tenancyList = data.d.tenancy_list;
    },
  },
};
</script>
